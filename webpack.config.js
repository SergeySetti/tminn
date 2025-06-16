const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
    entry: {
        main: [
            './frontend/js/index.js',
            './frontend/scss/main.scss'
        ]
    },
    output: {
        path: path.resolve(__dirname, 'app/static/core'),
        filename: 'js/[name].bundle.js',
        assetModuleFilename: 'images/[name][ext]'
    },
    module: {
        rules: [
            // JavaScript handling
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            // SCSS and CSS handling
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ]
            },
            // Image handling
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource'
            }
        ]
    },
    resolve: {
        extensions: ['.js']
    },
    plugins: [
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({
            filename: 'css/[name].css'
        }),
        new CopyPlugin({
            patterns: [
                {
                    from: "frontend/images",
                    to: "images"
                }
            ]
        })
    ],
    mode: 'development'
};
