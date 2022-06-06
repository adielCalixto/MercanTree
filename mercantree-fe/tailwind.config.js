module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: [ 
            {
                mercantree: {
                    primary: "#ffffff", //branco
                    secondary: "#48bb78", // verde logo
                    success: "#0B2044", // azul escuro
                    neutral: "#000000", // preto"
                    error: "#d90429", // vermelho
                    info: "#31CC19", //  verde
                    warning: "#ffc300", // amarelo
                    "base-100": "#ffffff", // branco
                    "base-200": "#e5e5e5", // cinza
                    "base-300": "#14213d", // azul escuro
                    "base-400": "#000000", // preto

                    
                    "--rounded-box": "0.225rem", // border radius rounded-box utility class, used in card and other large boxes
                    "--rounded-btn": ".225rem", // border radius rounded-btn utility class, used in buttons and similar element
                    "--rounded-badge": "1rem", // border radius rounded-badge utility class, used in badges and similar
                    "--animation-btn": "0.1s", // duration of animation when you click on button
                    "--animation-input": "0.1s", // duration of animation for inputs like checkbox, toggle, radio, etc
                    "--btn-text-case": "uppercase", // set default text transform for buttons
                    "--btn-focus-scale": "0.95", // scale transform of button when you focus on it
                    "--border-btn": "1px", // border width of buttons
                    "--tab-border": "1px", // border width of tabs
                    "--tab-radius": "0.5rem", // border radius of tabs
                    "border": "1px", //
                },
            },'business',
        ]
    }
}