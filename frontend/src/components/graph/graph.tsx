import React from "react";
import { useD3 } from "../../hooks/useD3";
import { getUniqueGroups } from "../../utils/utils";
import * as d3 from "d3";
import "../../css/style.css";
import { useAppSelector } from "../../app/hooks";
import {
  selectCurrentSearchedList,
  selectFilteredLinkData,
  selectFilteredNodeData,
} from "./graphSlice";
import { calculateChargeStrength, calculateZoom, consultantInitials, getCentralPoint, isSkillInSearchList, skillNameHTML } from "./utils";

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
          return isSkillInSearchList(d, currentSearchedList)
            ? "skillNodesHighlighted"
            : "skillNodes";
        });

      var skillNodeCircle = skillNode
        .append("circle")
        .attr("r", function (d: any) {
          return isSkillInSearchList(d, currentSearchedList) ? 10 : skillNodeRadius;
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
          return isSkillInSearchList(d, currentSearchedList) && "900";
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
              return isSkillInSearchList(d, currentSearchedList)
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
              return isSkillInSearchList(d, currentSearchedList)
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
            return (d.x += (getCentralPoint(d.group, groups, svgWidth, svgHeight)[0] - d.x) * k);
          })
          .attr("cy", function (d: any) {
            return (d.y += (getCentralPoint(d.group, groups, svgWidth, svgHeight)[1] - d.y) * k);
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
            return (d.x += (getCentralPoint(d.group, groups, svgWidth, svgHeight)[0] - d.x) * k);
          })
          .attr("cy", function (d: any) {
            return (d.y += (getCentralPoint(d.group, groups, svgWidth, svgHeight)[1] - d.y) * k);
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
            return isSkillInSearchList(d, currentSearchedList) ? d.y + 4 : d.y - 1;
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
