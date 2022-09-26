import React from "react"
import { useD3 } from "../../hooks/useD3"
import * as d3 from "d3"
import "../../css/style.css"

interface IGraphVis {
    data: any
}

function GraphVis({data}: IGraphVis) {
    const ref = useD3((svg: any) => {
        const width = 1000
        const height = 800

        var color = d3.scaleOrdinal(d3.schemePaired);

        // Add "forces" to the simulation here
        var simulation = d3.forceSimulation()
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("charge", d3.forceManyBody().strength(-30))
            .force("link", d3.forceLink().id(function(d: any) { return d.id; }).strength(0));

        simulation.force("r", d3.forceRadial(function(d: any) {
            if (d.group === "Consultant") {
                return 0
            }
            else {
                return 120
            }
            }, width/2, height/2)
        )

        // Add lines for every link in the dataset
        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(data.links)
            .enter().append("line")
                .attr("stroke-width", 1);

        // Add circles for every node in the dataset
        var node = svg.append("g")
            .attr("class", "nodes")

            
        var nodeCircle = node.selectAll("circle")
            .data(data.nodes)
            .enter().append("circle")
                    .attr("r", 13)
                    .attr("fill", function(d: any) { return color(d.group); })
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended)
                    );

        var nodeText = node.selectAll("text")
            .data(data.nodes)
            .enter().append("text")
                    .style("font-size", "8px")
                    .attr("text-anchor", "middle")
                    .text(function(d: any) {return d.name})

        // Basic tooltips
        nodeCircle.append("title")
            .text(function(d: any) { return d.name; });

        // Attach nodes to the simulation, add listener on the "tick" event
        simulation
            .nodes(data.nodes)
            .on("tick", ticked);

        // Associate the lines with the "link" force
        simulation.force<d3.ForceLink<any, any>>("link")?.links(data.links)
            
        // Dynamically update the position of the nodes/links as time passes
        function ticked() {
            link
                .attr("x1", function(d: any) { return d.source.x; })
                .attr("y1", function(d: any) { return d.source.y; })
                .attr("x2", function(d: any) { return d.target.x; })
                .attr("y2", function(d: any) { return d.target.y; });

            nodeCircle.attr("cx", function(d: any) { return d.x; })
                .attr("cy", function(d: any) { return d.y; });
                

            nodeText.attr("x", function(d: any) { return d.x; })
                .attr("y", function(d: any) { return d.y; });
                }

        // Change the value of alpha, so things move around when we drag a node
        function dragstarted(event: any, d: any) {
        if (!event.active) simulation.alphaTarget(0.9).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        // Fix the position of the node that we are looking at
        function dragged(event: any, d: any) {
            d.fx = event.x;
            d.fy = event.y;
        }

        // Let the node do what it wants again once we've looked at it
        function dragended(event: any, d: any) {
            if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
        }
    })

    return(
        <svg
            ref={ref}
            style={{
                height: 800,
                width: 1000
            }}
        />
    )
}


export default GraphVis