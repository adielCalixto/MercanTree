interface User {
    username: string,
    email: string,
    is_admin: boolean,
    id?: number,
    password: string,
}

interface LoggedUser {
    token: string,
    username: string,
    id?: number,
}

interface LoginUser {
    password: string,
    username: string,
}

export type { LoggedUser, LoginUser, User }