export type LogoutResponse = {
  isLoggedIn: boolean;
};

export type UserResponse = {
  userLoggedIn: boolean;
  userName: string;
  isAdmin: boolean;
};
