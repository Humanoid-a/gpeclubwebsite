const path = require('path');

module.exports = {
    entry: './static/assets/js/ai.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static/assets/js')
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }
        ]
    },
    resolve: {
        alias: {
            openai: path.resolve(__dirname, 'node_modules/openai')
        }
    }
};