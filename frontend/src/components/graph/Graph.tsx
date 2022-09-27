import React from "react"
import { useD3 } from "../../hooks/useD3"
import * as d3 from "d3"
import "../../css/style.css"

interface IGraphVis {
    data: any
}

function generateNameHTML(name: string, consultant: boolean = false) {
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
    return `<p style="text-align: center ${consultant && '; font-weight: 600'}">${trimmedName}</p>`
}

const width = 1000
const height = 800

function getCentralPoint(groupName: string) {
    if (groupName === "Consultant") {
        return [width/2, height/2]
    }
    else {
        const groups: Array<string> = [
            "Consultant",
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
        const x = width/2 + (height/2 - 350) * Math.cos((2 * i * Math.PI) / groups.length)
        const y = height/2 + (height/2 - 350) * Math.sin((2 * i * Math.PI) / groups.length)
        return [x, y]
    }
}


function GraphVis({data}: IGraphVis) {
    const ref = useD3((svg: any) => {

        var color = d3.scaleOrdinal(d3.schemePaired);

        // Add "forces" to the simulation here
        var simulation = d3.forceSimulation()
            .force("center", d3.forceCenter(width/2, height/2))
            .force("charge", d3.forceManyBody().strength(function(d: any) {
                const nameLength = d.name.length
                if (nameLength > 5) {
                    return -20 * nameLength
                }
                else {
                    return -80
                }
            }))
            .force("link", d3.forceLink().id(function(d: any) { return d.id; }).strength(0))
            .alphaDecay(0.05)

        // Add lines for every link in the dataset
        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(data.links)
            .enter().append("line")
                .attr("stroke-width", 1);

        // Add circles for every node in the dataset
        var node = svg.append("g")
            .selectAll("g")
            .data(data.nodes)
            .enter()
            .append("g")
                .attr("class", "nodes")

        const nodeRadius = 6;

        var nodeCircle = node.append("circle")
        .attr("r", nodeRadius)
        .attr("fill", function(d: any) { return color(d.group); })

        var nodeForeignObj = node.append("foreignObject")
            .attr("width", 60)
            .attr("height", 100)

        nodeForeignObj.append("xhtml:body")
            .style("font-size", "8px")
            .style("text-align", "center")
            .html(function(d: any) {return generateNameHTML(d.name, d.group==="Consultant")})   

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
            var k = simulation.alpha();

            nodeCircle.attr("cx", function(d: any) {return d.x += (getCentralPoint(d.group)[0] - d.x) * k;})
                .attr("cy", function(d: any) { return d.y += (getCentralPoint(d.group)[1] - d.y) * k;});
                

            nodeForeignObj.attr("x", function(d: any) { return d.x - 30; })
                .attr("y", function(d: any) { return d.y - 1; });

            link
                .attr("x1", function(d: any) { return d.source.x; })
                .attr("y1", function(d: any) { return d.source.y; })
                .attr("x2", function(d: any) { return d.target.x; })
                .attr("y2", function(d: any) { return d.target.y; });

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


export default GraphVis;