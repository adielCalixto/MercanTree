enum Theme {
    'DARK' = 'business',
    'LIGHT' = 'mercantree'
}

interface Config {
    theme: Theme;
    add_product_to_order_when_unique: boolean;
}

export default Config
export { Theme }