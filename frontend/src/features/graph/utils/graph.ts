import * as d3 from "d3";
import { categoryMap } from "../../../utils/skillCategories";

/**
 * Trim words in skill names that are greater than defined length.
 *
 * @param {string} name Name of skill.
 * @return {string} Name of skill with long words trimmed.
 */
export function processSkillName(name: string): string {
  const maxLength = 12;
  let trimmedName = "";
  const splitWords = name.split(" ");
  splitWords.forEach((word, i) => {
    if (word.length > maxLength) {
      trimmedName += word.substring(0, maxLength) + ".";
    } else {
      trimmedName += word;
    }
    if (i < splitWords.length - 1) {
      trimmedName += " ";
    }
  });
  return trimmedName;
}

/**
 * Trim skill name and wrap in centrally aligned HTML tag.
 *
 * @param {string} name Name of skill.
 * @return {string} HTML string of centrally aligned and trimmed skill name.
 */
export function skillNameHTML(name: string): string {
  const trimmedName = processSkillName(name);
  return `<center style="display: inline-flex;">${trimmedName}</center>`;
}

/**
 * Convert Consultant names to initials.
 *
 * @param {string} name Name of consultant.
 * @return {string} Initials of consultant.
 */
export function consultantInitials(name: string): string {
  let initials = "";
  const splitWords = name.trim().split(" ");
  splitWords.forEach((word) => {
    initials += word[0].toUpperCase();
  });
  return initials;
}

/**
 * Determine transform and scale for auto-zooming contents of viewport to svg.
 * Parameters have been adjusted to roughly work - may need further tweaking.
 *
 * @param {any} svg Root svg.
 * @param {any} svg Root svg-category.
 * @return {d3.ZoomTransform | undefined} If viewport larger than svg then zoom out, otherwise nothing to fit.
 */
export function calculateZoom(
  svg: any,
  rootGroup: any
): d3.ZoomTransform | undefined {
  // SVG dimensions
  var parent = svg.node().getBoundingClientRect();
  var fullWidth = parent.width,
    fullHeight = parent.height;

  // Viewport dimensions
  var bounds = rootGroup.node().getBoundingClientRect();
  var width = bounds.width,
    height = bounds.height;
  var midX = bounds.x + width / 2 - 500,
    midY = bounds.y + height / 2;

  // If viewport within svg then nothing to fit
  if (width < fullWidth - 100 && height < fullHeight - 100) return;

  // If viewport larger than svg then zoom out
  var widthScale = 0.85 / (width / fullWidth);
  var heightScale = 0.85 / (height / fullHeight);
  var scale = Math.min(widthScale, heightScale);
  var translate = [
    fullWidth / 2 - widthScale * midX,
    fullHeight / 2 - heightScale * midY,
  ];
  return d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale);
}

/**
 * Calculate repulsive charge strength of node.
 * If consultant, strength constant.
 * If skill, strength based on length of name.
 *
 * @param {any} node Node object from graph.
 * @return {number} Repulsive charge strength should be negative.
 */
export function calculateChargeStrength(node: any): number {
  const trimmedName = processSkillName(node.name);
  const nameLength = trimmedName.length;
  if (node.type == "Consultant") {
    return -200;
  } else if (nameLength > 20) {
    return -40 * nameLength;
  } else {
    return -700;
  }
}

/**
 * Get dimensions of cluster central point for a defined node category.
 *
 * @param {string} category Name of node category.
 * @return {number[]} x and y coordinates of node category central point.
 */
export function getCentralPoint(
  type: string,
  category: string,
  categories: Array<string>,
  svgWidth: number,
  svgHeight: number
): number[] {
  if (type === "Consultant") {
    // Consultant nodes in center
    return [svgWidth / 2, svgHeight / 2];
  } else {
    // Skill node central points distributed along ellipse around center
    // (xk, yk) = (x0 + rcos(2kπ/n), y0 + rsin(2kπ/n)) for k=0 to n−1
    const i = categories.indexOf(category);
    const x =
      svgWidth / 2 +
      (svgHeight / 2 - 350) * Math.cos((2 * i * Math.PI) / categories.length);
    const y =
      svgHeight / 2 +
      (svgHeight / 2 - 350) * Math.sin((2 * i * Math.PI) / categories.length);
    return [x, y];
  }
}

/**
 * Check if provided skill is in searched node list.
 *
 * @param {any} node Node object from graph.
 * @return {boolean} If provided skill node is a currently searched node.
 */
export function isSkillInSearchList(
  node: any,
  currentSearchedList: any[]
): boolean {
  return (
    currentSearchedList.filter(function (s: any) {
      return s.name === node.name;
    }).length > 0
  );
}

export const nodeColor = (type: string, category: string) => {
  if (type === "Consultant") {
    return "#c0d2f0";
  } else {
    return categoryMap[category].color.slice(0, -2) + "80";
  }
};
