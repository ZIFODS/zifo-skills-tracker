import axios from "axios";
import { Buffer } from "buffer";

let baseURL = "ec2-35-176-61-224.eu-west-2.compute.amazonaws.com";
baseURL = "localhost"; // comment if deploying

export default class GraphDataService {
  // GET request of all graph data.
  public static fetchGraphData = () =>
    axios({
      method: "get",
      url: `http://${baseURL}:8080/skills`,
    });

  // GET request of graph data filtered by skill and with groups hidden.
  public static filterGraphData(skills: string[], hiddenGroups: string[]) {
    const skillsQuery = Buffer.from(JSON.stringify(skills)).toString("base64");
    let url = `http://${baseURL}:8080/consultants/?skills=${skillsQuery}`;

    if (hiddenGroups.length > 0) {
      const hiddenGroupsQuery = hiddenGroups.join("&hidden_groups=");
      url = url + `&hidden_groups=${hiddenGroupsQuery}`;
    }

    return axios({
      method: "get",
      url: url,
    });
  }
}
