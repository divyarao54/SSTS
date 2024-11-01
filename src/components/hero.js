import { Link } from 'react-router-dom';
import heroImg from '../assets/heroImage.jpg';
import './styles/hero.css'
const Hero = () => {
    return(
        <div className="hero-section">
            <img className="hero-img" alt="hero-img" src={heroImg}/>

            <div className='hero-text'>
                <div className='hero-title'>Empower Your Learning Journey</div>
                <div className='hero-desc'>Track your skills, set goals, and see your progress. Achieve more with a tool designed to help you grow!</div>
                <Link to='/login' style={{maxWidth: 'fit-content'}}>
                    <button className='hero-button'>GET STARTED</button>
                </Link>
            </div>
        </div>
    );
}

export default Hero;