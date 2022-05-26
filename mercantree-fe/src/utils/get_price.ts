export default function get_price(price: string): string {
    return `R$${parseFloat(price).toFixed(2)}`
}