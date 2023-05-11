function testFunc(){
    alert("Button Clicked")
}

function buildHeader(){
    const header = `
    <header>
        <nav>
            <ul>
                <li><a href="./home.html">Home</a>
                    <ul>
                        <li><a href="./about.html">About</a></li>
                        <li><a href="./blog.html">Blog</a></li>
                    </ul>
                </li>

                <li><a href="#">Dashboards</a>
                    <ul>
                        <li><a href="./dashboards/spotify.html">Spotify</a></li>
                        <li><a href="./dashboards/strava.html">Strava</a></li>
                        <li><a href="./dashboards/untappd.html">Untappd</a></li>
                    </ul>
                </li>
                <li><a href="#">Art</a>
                    <ul>
                        <li><a href="./photo.html">Photography</a></li>
                        <li><a href="./astrosites.html">Astro</a></li>
                    </ul>
                <li><a href="#">Contact</a></li>
            </ul>
        </nav>
    </header>
    `;
    document.write(header)
}