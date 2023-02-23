export type CategoryMap = {
  [key: string]: {
    displayName: string;
    color: string;
  };
};

export const categoryMap: CategoryMap = {
  Service: {
    displayName: "Services",
    color: "#9013FE20",
  },
  Methodology: {
    displayName: "Methodologies",
    color: "#41750520",
  },
  Scientific_Products_And_Applications: {
    displayName: "Scientific Products & Applications",
    color: "#4A4A4A20",
  },
  R_And_D_Processes: {
    displayName: "R&D Processes",
    color: "#4A90E220",
  },
  Products_And_Applications: {
    displayName: "Products and Applications",
    color: "#A16C1D20",
  },
  Regulation: {
    displayName: "Regulatory",
    color: "#D0021B20",
  },
  Data_Management: {
    displayName: "Data Management",
    color: "#7ED32120",
  },
  Languages: {
    displayName: "Languages",
    color: "#F0C41920",
  },
  Programming_languages: {
    displayName: "Programming Languages",
    color: "#3B247820",
  },
  Miscellaneous: {
    displayName: "Miscellaneous",
    color: "#FFFFFF20",
  },
  Infrastructure_Technologies: {
    displayName: "Infrastructure Technologies",
    color: "#50E3C220",
  },
};
