import axios from "axios";
import { Buffer } from "buffer";

let baseURL = "ec2-35-176-61-224.eu-west-2.compute.amazonaws.com";
baseURL = "localhost"; // comment if deploying

export default class GraphDataService {
  // GET request of all graph data.
  public static fetchGraphData = () =>
    axios({
      method: "get",
      url: `http://${baseURL}:8080/all`,
    });

  // GET request of graph data filtered by skill and with groups hidden.
  public static filterGraphDataWithSkills(skills: string[], hiddenGroups: string[] = []) {
    const skillsQuery = Buffer.from(JSON.stringify(skills)).toString("base64");
    let url = `http://${baseURL}:8080/skills/?skills=${skillsQuery}`;

    if (hiddenGroups !== undefined) {
      if (hiddenGroups.length > 0) {
        const hiddenGroupsQuery = hiddenGroups.join("&hidden_categories=");
        url = url + `&hidden_categories=${hiddenGroupsQuery}`;
      }
    }

    return axios({
      method: "get",
      url: url,
    });
  }

  // GET request of graph data filtered by consultant
  public static filterGraphDataByConsultant(consultant: string, hiddenGroups: string[] = []) {
    let url = `http://${baseURL}:8080/consultant/?consultant_name=${consultant}`;

    if (hiddenGroups !== undefined) {
      if (hiddenGroups.length > 0) {
        const hiddenGroupsQuery = hiddenGroups.join("&hidden_categories=");
        url = url + `&hidden_categories=${hiddenGroupsQuery}`;
      }
    }

    return axios({
      method: "get",
      url: url,
    });
  }
}
