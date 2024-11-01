import { Link } from 'react-router-dom';
import htoeImg from '../assets/htoeImg.png';
import './styles/htoe.css'

const HToE = () => {
    return(
        <div className="htoe-section">
            <div className="htoe-img">
                <img alt="htoe-img" className='htoe-img' src={htoeImg}/>
            </div>
            <div className="htoe-text">
                <div className="htoe-title">Unleash Your Potential with Exciting Events!</div>
                <div className="htoe-desc">Ready to put your skills to the test and learn something new? Dive into hands-on experiences with the latest events — from hackathons and workshops to quizzes and ideathons! Connect with like-minded peers, challenge yourself, and unlock new possibilities. Join the excitement and make every event a step toward your future success!</div>
                <Link to = "/events" style={{maxWidth: 'fit-content'}}>
                    <button className='htoe-button'>EXPLORE EVENTS</button>
                </Link>
            </div>

        </div>
    );
}

export default HToE;