import axios from "axios";

export default class GraphDataService {
  public static fetchGraphData = () =>
    axios({
      method: "get",
      url: "http://localhost:8080/skills",
    });
}