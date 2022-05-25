import axios from '../boot/axios'
import { LoginUser } from '../interfaces/users/user.interface';
import errorService from './errorService';

class AuthService {
  login(user: LoginUser) {
    return axios
      .post('api-auth/', {
        username: user.username,
        password: user.password
      })
      .then(response => {
        return Promise.resolve(response.data);
      })
      .catch(error => {
        errorService().onError(error)
        return Promise.reject(error);
      })
  }
}
  
export default new AuthService();