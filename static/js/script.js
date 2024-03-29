let slider = tns({
    container : ".my-slider",
    "slideBy" : "1",
    "speed" : 1500,
    "nav" : false,
    controlsPosition: "bottom",
    navPosition: "bottom",
    autoplay: true,
    autoplayButtonOutput: false,
    controlsContainer: "#custom-control",
    responsive: {
        1600: {
            items : 6,
            gutter : 20
        },
        1024: {
            items: 5,
            gutter: 20
        },
        768: {
            items: 4,
            gutter: 20
        },
        480: {
            items: 3,
            gutter: 20
        },
    }
})