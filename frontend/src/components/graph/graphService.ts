import axios from "axios";

export default class GraphDataService {
  public static fetchGraphData = () =>
    axios({
      method: "get",
      url: "http://localhost:8080/skills",
    });

    public static filterGraphData (skills: string[]) {
      const skillsQuery = skills.join("&skills=")
      return axios({
        method: "get",
        url: `http://localhost:8080/consultants/?skills=${skillsQuery}`,
      });
  }
}