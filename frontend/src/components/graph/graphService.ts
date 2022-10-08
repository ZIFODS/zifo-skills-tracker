import axios from "axios";

export default class GraphDataService {
  public static fetchGraphData = () =>
    axios({
      method: "get",
      url: "http://localhost:8080/skills",
    });

  public static filterGraphData (skills: string[], hiddenGroups: string[]) {
    const skillsQuery = skills.join("&skills=")
    let url = `http://localhost:8080/consultants/?skills=${skillsQuery}`

    if (hiddenGroups.length > 0) {
      const hiddenGroupsQuery = hiddenGroups.join("&hidden_groups=")
      url = url + `&hidden_groups=${hiddenGroupsQuery}`
    }
    
    return axios({
      method: "get",
      url: url,
    });
  }
}