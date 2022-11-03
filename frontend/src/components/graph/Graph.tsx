import React from "react";
import { getUniqueGroups, useD3 } from "../../hooks/useD3";
import * as d3 from "d3";
import "../../css/style.css";
import { useAppSelector } from "../../app/hooks";
import {
  selectCurrentSearchedList,
  selectFilteredLinkData,
  selectFilteredNodeData,
} from "./graphSlice";

/**
 * Trim words in skill names that are greater than defined length.
 *
 * @param {string} name Name of skill.
 * @return {string} Name of skill with long words trimmed.
 */
function processSkillName(name: string): string {
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
function skillNameHTML(name: string): string {
  const trimmedName = processSkillName(name);
  return `<center style="display: inline-flex;">${trimmedName}</center>`;
}

/**
 * Convert Consultant names to initials.
 *
 * @param {string} name Name of consultant.
 * @return {string} Initials of consultant.
 */
function consultantInitials(name: string): string {
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
 * @param {any} svg Root svg-group.
 * @return {d3.ZoomTransform | undefined} If viewport larger than svg then zoom out, otherwise nothing to fit.
 */
function calculateZoom(svg: any, rootGroup: any): d3.ZoomTransform | undefined {
  // SVG dimensions
  var parent = svg.node().getBoundingClientRect();
  var fullWidth = parent.width,
    fullHeight = parent.height;

  // Viewport dimensions
  var bounds = rootGroup.node().getBoundingClientRect();
  var width = bounds.width,
    height = bounds.height;
  var midX = bounds.x + width / 2 - 700,
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
const calculateChargeStrength = (node: any) => {
  const trimmedName = processSkillName(node.name);
  const nameLength = trimmedName.length;
  if (node.group == "Consultant") {
    return -200;
  } else if (nameLength > 20) {
    return -40 * nameLength;
  } else {
    return -700;
  }
};

/**
 * SVG containing d3 force directed graph.
 */
function GraphVis() {
  // Nodes and links
  var nodeData = useAppSelector(selectFilteredNodeData);
  var linkData = useAppSelector(selectFilteredLinkData);

  // Copy data due to useAppSelector type issues with d3
  nodeData = JSON.parse(JSON.stringify(nodeData));
  linkData = JSON.parse(JSON.stringify(linkData));

  // Groups
  const groups = getUniqueGroups(nodeData);

  // Searched nodes
  const currentSearchedList = useAppSelector(selectCurrentSearchedList);

  /**
   * Check if provided skill is in searched node list.
   *
   * @param {any} node Node object from graph.
   * @return {boolean} If provided skill node is a currently searched node.
   */
  const isSkillInSearchList = (node: any): boolean => {
    return (
      currentSearchedList.filter(function (s: any) {
        return s.name === node.name;
      }).length > 0
    );
  };

  const ref = useD3(
    (svg: any) => {
      // Assign colours to each node group in data
      const color = d3.scaleOrdinal().domain(groups).range(d3.schemePaired);

      // Remove all existing svg-groups on svg
      svg.selectAll("g").remove();

      // Create single root svg-group
      const rootGroup = svg.append("g");
      rootGroup.attr("transform", undefined); // TODO: needed?

      // Get current dimensions of svg
      var parent = svg.node().parentElement;
      var svgWidth = parent.clientWidth;
      var svgHeight = parent.clientHeight;

      // Dimensions of Zifo logo
      const imgWidth = 100;
      const imgHeight = 50;
      const imgMargin = 10;

      // Add Zifo logo at bottom right of screen
      svg
        .append("svg:image")
        .attr("xlink:href", require("../../images/zifo-logo.png"))
        .attr("x", svgWidth - imgWidth - imgMargin)
        .attr("y", svgHeight - imgHeight - imgMargin)
        .attr("width", imgWidth)
        .attr("height", imgHeight);

      /**
       * Get dimensions of cluster central point for a defined node group.
       *
       * @param {string} groupName Name of node group.
       * @return {number[]} x and y coordinates of node group central point.
       */
      const getCentralPoint = (groupName: string): number[] => {
        if (groupName === "Consultant") {
          // Consultant nodes in center
          return [svgWidth / 2, svgHeight / 2];
        } else {
          // Skill node central points distributed along ellipse around center
          // (xk, yk) = (x0 + rcos(2kπ/n), y0 + rsin(2kπ/n)) for k=0 to n−1
          const i = groups.indexOf(groupName);
          const x =
            svgWidth / 2 +
            (svgHeight / 2 - 350) * Math.cos((2 * i * Math.PI) / groups.length);
          const y =
            svgHeight / 2 +
            (svgHeight / 2 - 350) * Math.sin((2 * i * Math.PI) / groups.length);
          return [x, y];
        }
      };

      // Add "forces" to the simulation here
      var simulation = d3
        .forceSimulation()
        .force(
          "charge",
          d3.forceManyBody().strength(function (d: any) {
            return calculateChargeStrength(d);
          })
        )
        .force(
          "link",
          d3
            .forceLink()
            .id(function (d: any) {
              return d.id;
            })
            .strength(0)
        );

      // Add lines for every link in the dataset
      var linkG = rootGroup
        .selectAll("g.links")
        .data(linkData, function (d: any) {
          return d.id;
        });

      const link = linkG.enter().append("g").attr("class", "links");

      const linkLine = link.append("line").attr("stroke-width", 1);

      // Nodes for consultants
      const consultantNodeRadius = 14;

      var consultantG = rootGroup.selectAll("g.consultNodes").data(
        nodeData.filter(function (d: any) {
          return d.group === "Consultant";
        }),
        function (d: any) {
          return d.id;
        }
      );

      const consultantNode = consultantG
        .enter()
        .append("g")
        .attr("class", "consultNodes");

      var consultantNodeCircle = consultantNode
        .append("circle")
        .attr("r", consultantNodeRadius)
        .attr("fill", function (d: any) {
          return color(d.group);
        });

      var consultantNodeText = consultantNode
        .append("text")
        .text(function (d: any) {
          return consultantInitials(d.name);
        })
        .style("text-anchor", "middle");

      // Nodes for skills
      const skillNodeRadius = 6;

      var skillG = rootGroup
        .selectAll("g.skillNodes, g.skillNodesHighlighted")
        .data(
          nodeData.filter(function (d: any) {
            return d.group !== "Consultant";
          }),
          function (d: any) {
            return d.id;
          }
        );

      const skillNode = skillG
        .enter()
        .append("g")
        .attr("class", function (d: any) {
          return isSkillInSearchList(d)
            ? "skillNodesHighlighted"
            : "skillNodes";
        });

      var skillNodeCircle = skillNode
        .append("circle")
        .attr("r", function (d: any) {
          return isSkillInSearchList(d) ? 10 : skillNodeRadius;
        })
        .attr("fill", function (d: any) {
          return color(d.group);
        });

      var skillNodeText = skillNode
        .append("foreignObject")
        .attr("class", "foreignObject")
        .attr("width", 1)
        .attr("height", 1);

      skillNodeText
        .append("xhtml:body")
        .style("font-size", "10px")
        .style("font-weight", function (d: any) {
          return isSkillInSearchList(d) && "900";
        })
        .style("font-family", "helvetica")
        .style("position", "relative")
        .style("z-index", 5)
        .html(function (d: any) {
          return skillNameHTML(d.name);
        });

      // Consultant tooltip div
      var div = d3
        .select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

      // Hovering mouse over consultant node
      consultantNode
        .on("mouseover", function (event: any, d: any) {
          const linkedSkills = link.filter(function (l: any) {
            return l.source.id === d.id || l.target.id === d.id;
          })._groups[0];
          const linkedSkillIds = linkedSkills.map(function (g: any) {
            return g.__data__.target.id;
          });
          link
            .filter(function (l: any) {
              return l.source.id === d.id || l.target.id === d.id;
            })
            .attr("class", "linksSelected");
          link
            .filter(function (l: any) {
              return l.source.id !== d.id && l.target.id !== d.id;
            })
            .attr("class", "linksDeselected");
          consultantNode
            .filter(function (node: any) {
              return node.id !== d.id;
            })
            .attr("class", "consultNodesDeselected");
          skillNode
            .filter(function (node: any) {
              return !linkedSkillIds.includes(node.id);
            })
            .attr("class", "skillNodesDeselected")
            .select("foreignObject")
            .style("opacity", "0.1");
          skillNode
            .filter(function (node: any) {
              return linkedSkillIds.includes(node.id);
            })
            .select("foreignObject")
            .style("font-weight", "bold");
          div.transition().duration(200).style("opacity", 1);
          div
            .html(d.name.split(" ").join("<br/>"))
            .style("left", event.pageX + "px")
            .style("top", event.pageY + "px");
        })
        .on("mouseout", function (d: any) {
          link.attr("class", "links");
          consultantNode.attr("class", "consultNodes");
          skillNode
            .attr("class", function (d: any) {
              return isSkillInSearchList(d)
                ? "skillNodesHighlighted"
                : "skillNodes";
            })
            .select("foreignObject")
            .style("opacity", "1")
            .style("font-weight", "normal");
          div.transition().duration(500).style("opacity", 0);
        });

      // Hovering mouse over skill node
      skillNode
        .on("mouseover", function (event: any, d: any) {
          const linkedConsultants = link.filter(function (l: any) {
            return l.source.id === d.id || l.target.id === d.id;
          })._groups[0];
          const linkedConsultantIds = linkedConsultants.map(function (g: any) {
            return g.__data__.source.id;
          });
          link
            .filter(function (l: any) {
              return l.source.id === d.id || l.target.id === d.id;
            })
            .attr("class", "linksSelected");
          link
            .filter(function (l: any) {
              return l.source.id !== d.id && l.target.id !== d.id;
            })
            .attr("class", "linksDeselected");
          consultantNode
            .filter(function (node: any) {
              return !linkedConsultantIds.includes(node.id);
            })
            .attr("class", "consultNodesDeselected");
          skillNode
            .filter(function (node: any) {
              return node.id !== d.id;
            })
            .attr("class", "skillNodesDeselected")
            .select("foreignObject")
            .style("opacity", "0.1");
          skillNode
            .filter(function (node: any) {
              return node.id === d.id;
            })
            .select("foreignObject")
            .style("font-weight", "bold");
        })
        .on("mouseout", function (d: any) {
          link.attr("class", "links");
          consultantNode.attr("class", "consultNodes");
          skillNode
            .attr("class", function (d: any) {
              return isSkillInSearchList(d)
                ? "skillNodesHighlighted"
                : "skillNodes";
            })
            .select("foreignObject")
            .style("opacity", "1")
            .style("font-weight", "normal");
        });

      // Attach nodes to the simulation, add listener on the "tick" event
      simulation.nodes(nodeData).on("tick", ticked);

      // Associate the lines with the "link" force
      simulation.force<d3.ForceLink<any, any>>("link")?.links(linkData);

      // Set parameters for simulation and start
      simulation.alpha(1).alphaDecay(0.05).restart();

      /**
       * Dynamically update the position of the nodes/links as time passes.
       * Apply zoom change once when simulation has cooled to a certain point.
       */
      var zoomed = false;
      function ticked() {
        var k = simulation.alpha();

        consultantNodeCircle
          .attr("cx", function (d: any) {
            return (d.x += (getCentralPoint(d.group)[0] - d.x) * k);
          })
          .attr("cy", function (d: any) {
            return (d.y += (getCentralPoint(d.group)[1] - d.y) * k);
          });

        consultantNodeText
          .attr("x", function (d: any) {
            return d.x;
          })
          .attr("y", function (d: any) {
            return d.y + 3;
          });

        skillNodeCircle
          .attr("cx", function (d: any) {
            return (d.x += (getCentralPoint(d.group)[0] - d.x) * k);
          })
          .attr("cy", function (d: any) {
            return (d.y += (getCentralPoint(d.group)[1] - d.y) * k);
          });

        skillNodeText
          .attr("x", function (d: any) {
            const width = skillNode
              .filter(function (s: any) {
                return d.id === s.id;
              })
              .select("foreignObject")._groups[0][0].children[0].scrollWidth;
            return d.x - width / 2 - 8;
          })
          .attr("y", function (d: any) {
            return isSkillInSearchList(d) ? d.y + 4 : d.y - 1;
          });

        linkLine
          .attr("x1", function (d: any) {
            return d.source.x;
          })
          .attr("y1", function (d: any) {
            return d.source.y;
          })
          .attr("x2", function (d: any) {
            return d.target.x;
          })
          .attr("y2", function (d: any) {
            return d.target.y;
          });

        if (k < 0.15) {
          if (zoomed === false) {
            var transform = calculateZoom(svg, rootGroup);
            rootGroup.transition().duration(500).attr("transform", transform);
            zoomed = true;
          }
        }
      }
    },
    [nodeData, linkData]
  );

  return <svg ref={ref} height="100%" width="100%" />;
}

export default GraphVis;
