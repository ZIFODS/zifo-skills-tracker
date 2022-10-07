import React from "react"
import { useD3 } from "../../hooks/useD3"
import * as d3 from "d3"
import "../../css/style.css"
import { useAppDispatch, useAppSelector } from "../../app/hooks"
import { getGraphDataRequest, selectCurrentLinks, selectCurrentNodes } from "./graphSlice"
import { useEffect } from "react";
import { SimulationNodeDatum } from "d3"
import graphData from "../../data/d3_skills.json"
import { useSelector } from "react-redux"

function skillNameHTML(name: string) {
    let trimmedName = ""
    const splitWords = name.split(" ")
    splitWords.forEach((word, i) => {
        if (word.length > 12) {
            trimmedName += word.substring(0, 10) + "."
        }
        else {
            trimmedName += word
        }
        if (i < splitWords.length - 1) {
            trimmedName += " "
        }
    })
    return `<p style="text-align: center;">${trimmedName}</p>`
}

function consultantNameHTML(name: string) {
    let initials = ""
    const splitWords = name.split(" ")
    splitWords.forEach((word) => {
        initials += word[0].toUpperCase()
    })
    return `<p style="text-align: center; font-weight: 700">${initials}</p>`
}

function GraphVis() {
    const dispatch = useAppDispatch();

    useEffect(() => {
        dispatch(getGraphDataRequest());
      }, [dispatch]);

    var nodeData = useAppSelector(selectCurrentNodes);
    var linkData = useAppSelector(selectCurrentLinks);

    nodeData = JSON.parse(JSON.stringify(nodeData))
    linkData = JSON.parse(JSON.stringify(linkData))

    // nodeData = graphData.nodes
    // linkData = graphData.links

    const ref = useD3((svg: any) => {

        const t = d3.transition().duration(250)

        var color = d3.scaleOrdinal(d3.schemePaired);

        var parent = svg.node().parentElement;
        var svgWidth = parent.clientWidth;
        var svgHeight = parent.clientHeight;

        console.log(svg.node().getBoundingClientRect())

        const getCentralPoint = (groupName: string) => {
            if (groupName === "Consultant") {
                return [svgWidth/2, svgHeight/2]
            }
            else {
                const groups: Array<string> = [
                    "ScienceApps",
                    "Services",
                    "Methodologies",
                    "Process",
                    "Other_Products",
                    "Regulatory",
                    "Data_Management",
                    "Languages",
                    "programming",
                    "Miscellaneous",
                    "Infrastructure"
                ]
                const i = groups.indexOf(groupName)
                // (xk,yk)=(x0+rcos(2kπ/n),y0+rsin(2kπ/n)) for k=0 to n−1.
                const x = svgWidth/2 + (svgHeight/2 - 300) * Math.cos((2 * i * Math.PI) / groups.length)
                const y = svgHeight/2 + (svgHeight/2 - 300) * Math.sin((2 * i * Math.PI) / groups.length)
                return [x, y]
            }
        }

        // Add "forces" to the simulation here
        var simulation = d3.forceSimulation()
            .force("center", d3.forceCenter(svgWidth/2, svgHeight/2))
            .force("charge", d3.forceManyBody().strength(function(d: any) {
                const nameLength = d.name.length
                if (d.group == "Consultant") {
                    return -160
                }
                else if (nameLength > 5) {
                    return -20 * nameLength
                }
                else {
                    return -120
                }
            }))
            .force("link", d3.forceLink().id(function(d: any) { return d.id; }).strength(0))

        // Add lines for every link in the dataset
        svg
            .selectAll("g.links")
                .remove()

        var linkG = svg
            .selectAll("g.links")
            .data(linkData, function(d: any) {return d.id})

        const link = linkG.enter()
            .append("g")
            .attr("class", "links")

        const linkLine = link.append("line")
            .attr("stroke-width", 1);

        // Nodes for consultants
        const consultantNodeRadius = 12;

        svg
        .selectAll("g.consultNodes")
            .remove()

        var consultantG = svg
            .selectAll("g.consultNodes")
            .data(nodeData.filter(function(d: any) {return d.group==="Consultant"}), function(d: any) {return d.id})

        const consultantNode = consultantG.enter()
            .append("g")
                .attr("class", "consultNodes")

        var consultantNodeCircle = consultantNode.append("circle")
            .attr("r", consultantNodeRadius)
            .attr("fill", function(d: any) { return color(d.group); })

        consultantNodeCircle.append("title")
            .text(function(d: any) { return d.name; });

        var consultantNodeText = consultantNode.append("foreignObject")
            .attr("width", 60)
            .attr("height", 50)

        consultantNodeText.append("xhtml:body")
            .style("font-size", "8px")
            .style("text-align", "center")
            .html(function(d: any) {return consultantNameHTML(d.name)}) 

        // Nodes for skills
        const skillNodeRadius = 6;

        svg
            .selectAll("g.skillNodes")
                .remove()

        var skillG = svg
            .selectAll("g.skillNodes")
            .data(nodeData.filter(function(d: any) {return d.group!=="Consultant"}), function(d: any) {return d.id})

        const skillNode = skillG.enter()
            .append("g")
                .attr("class", "skillNodes")

        var skillNodeCircle = skillNode.append("circle")
            .attr("r", skillNodeRadius)
            .attr("fill", function(d: any) { return color(d.group); })

        skillNodeCircle.append("title")
        .text(function(d: any) { return d.name; });

        var skillNodeText = skillNode.append("foreignObject")
            .attr("width", 60)
            .attr("height", 100)

        skillNodeText.append("xhtml:body")
            .style("font-size", "8px")
            .style("text-align", "center")
            .html(function(d: any) {return skillNameHTML(d.name)})

        var div = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);
            
        consultantNode.on("mouseover", function(event: any, d: any) {
            // link
            //     .filter(function(l: any) {return l.source.id === d.id || l.target.id === d.id})
            //     .attr("class", "linksSelected")
            // skillNode
            //     .filter(function(node: any) {return node.id === d.id})
            //     .style("visibility", "hidden");
            //   })
            //   .on("mouseout", function(event: any, d: any) {
            //     link
            //     .filter(function(node: any) {return node.source.id !== d.id && node.target.id !== d.id})
            //     .style("visibility", "visible")
            //     skillNode
            //     .filter(function(node: any) {return node.id === d.id})
            //     .style("visibility", "visible");
            //   });
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div.html(d.name.split(" ").join("<br/>"))
                .style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", function(d: any) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
            });

        // Attach nodes to the simulation, add listener on the "tick" event
        simulation
            .nodes(nodeData)
            .on("tick", ticked)

        // Associate the lines with the "link" force
        simulation.force<d3.ForceLink<any, any>>("link")?.links(linkData) 
        
        simulation
            .alpha(1)
            .alphaDecay(0.05)
            .restart();

        // Dynamically update the position of the nodes/links as time passes
        function ticked() {
            var k = simulation.alpha();

            consultantNodeCircle.attr("cx", function(d: any) {return d.x += (getCentralPoint(d.group)[0] - d.x) * k;})
                .attr("cy", function(d: any) { return d.y += (getCentralPoint(d.group)[1] - d.y) * k;});
                
            consultantNodeText.attr("x", function(d: any) { return d.x - 30; })
                .attr("y", function(d: any) { return d.y - 14; });

            skillNodeCircle.attr("cx", function(d: any) {return d.x += (getCentralPoint(d.group)[0] - d.x) * k;})
                .attr("cy", function(d: any) { return d.y += (getCentralPoint(d.group)[1] - d.y) * k;});
                
            skillNodeText.attr("x", function(d: any) { return d.x - 30; })
                .attr("y", function(d: any) { return d.y - 1; });

            linkLine
                .attr("x1", function(d: any) { return d.source.x; })
                .attr("y1", function(d: any) { return d.source.y; })
                .attr("x2", function(d: any) { return d.target.x; })
                .attr("y2", function(d: any) { return d.target.y; });
        }
    },
    [nodeData, linkData]
    )

    return(
        <svg
            ref={ref}
        />
    )
}


export default GraphVis;