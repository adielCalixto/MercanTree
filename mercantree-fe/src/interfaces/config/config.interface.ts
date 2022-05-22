enum Theme {
    'DARK' = 'business',
    'LIGHT' = 'corporate'
}

interface Config {
    theme: Theme;
    add_product_to_order_when_unique: boolean;
}

export default Config
export { Theme }