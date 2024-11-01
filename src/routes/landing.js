import Hero from "../components/hero";
import HToC from "../components/htoc";
import HToE from "../components/htoe";
import NavBar from "../components/navbar";

const LandingPage = () =>{
    return(
        <div style={{display: 'flex', flexDirection: 'column', gap: '150px', overflow: 'hidden'}}>
            <div>
                <NavBar/>
                <Hero />
            </div>
            <div>
                <HToE />
            </div>
            <div>
                <HToC />
            </div>
            
        </div>
    );
}

export default LandingPage;