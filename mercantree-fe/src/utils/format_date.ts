export default function (data: string) {
    return new Date(data).toLocaleDateString("pt-BR", { year: 'numeric', month: 'short', day: 'numeric' });
}