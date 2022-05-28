export default function (data?: string) {
    if (!data)
        return '---'

    return new Date(data).toLocaleDateString("pt-BR", { year: 'numeric', month: 'short', day: 'numeric' });
}