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
                    primary: "#245E8A",
                    secondary: "#40719C",
                    success: "#6DECAF",
                    neutral: "#122A3B",
                    error: "#F25F5C",
                    info: "#6470FA",
                    warning: "#F2CD5D",
                    "base-100": "#ffffff",
                    "base-200": "#f7f7f7",
                    "base-300": "#DDDDDD",
                    
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
                },
            },
            'business',
        ]
    }
}