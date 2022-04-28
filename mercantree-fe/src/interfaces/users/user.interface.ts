interface User {
    username: String,
    email: String,
    is_admin: Boolean,
    id?: Number,
    password: String,
}

interface LoggedUser {
    token: String,
    username: String,
    id: Number|undefined,
}

interface LoginUser {
    password: String,
    username: String,
}

export type { LoggedUser, LoginUser, User }