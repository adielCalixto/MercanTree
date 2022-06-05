import { AxiosError } from "axios"
import swal from "sweetalert"
import router from "../router"

export default function() {
    const onError = (error: AxiosError) => {
        const response = error.response
        
        if(response && response.status >= 400 && response.status < 405) {
            switch(response.status) {
                case 400:
                    swal('Requisição inválida. Verifique os dados.', `${error.message} - ${error.code ?? ''}`, 'error')
                break;

                case 401:
                    swal('Usuário não autenticado', `${error.message} - ${error.code ?? ''}`, 'error')
                    .then(() => {
                        router.push('/login')
                    })
                break;

                case 403:
                    swal('Você não tem permissão para realizar essa ação', `${error.message} - ${error.code ?? ''}`, 'error')
                    .then(() => {
                        router.go(-1)
                    })
                break;

                case 404:
                    swal('Servidor não encontrado.', `${error.message} - ${error.code ?? ''}`, 'error')
                    .then(() => {
                        router.push('/login')
                    })
                break;
            }
            
            return false
        }

        swal('Algum erro ocorreu :(', `${error.message} - ${error.code ?? ''}`, 'error')
    }

    const onWarn = async (title = "Tem certeza?", text= "Essa ação não pode ser revertida!") => {
        return swal({
            title,
            text,
            icon: "warning",
            buttons: {
                confirm: {
                    text: 'OK'
                },
                cancel: true,                
            },
            dangerMode: true,
            })
            .then(async (confirm) => {
                if (confirm) {
                    return Promise.resolve(confirm)
                }

                return Promise.reject(false)
            })
    }

    const onInfo = () => {


    }

    return {
        onError,
        onWarn,
        onInfo,
    }
}