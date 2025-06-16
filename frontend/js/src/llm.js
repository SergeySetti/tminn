export default () => ({
    init() {
        console.log('LLM initialized');
    },

    thinking: false,

    toggle() {
        this.thinkink = !this.thinking;
    },

    request() {
        this.thinking = true;
        // pause for 2 seconds
        setTimeout(() => {
            fetch('https://jsonplaceholder.typicode.com/posts/1')
                .then(response => response.json())
                .then(json => {
                    console.log(json)
                    this.thinking = false;
                })
        }, 2000);
    }
})
