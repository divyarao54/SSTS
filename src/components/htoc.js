import { Link } from 'react-router-dom';
import htocImg from '../assets/htocImg.png';
import './styles/htoc.css'

const HToC = () => {
    return(
        <div className="htoc-section">

            <div className="htoc-text">
                <div className="htoc-title">Level Up with Expert-Led Courses!</div>
                <div className="htoc-desc">Take charge of your learning journey with courses designed to boost your skills and confidence. Whether you're diving into something new or mastering your expertise, gain hands-on knowledge and practical insights. Join today and make every lesson count toward your success!</div>
                <Link to = "/courses" style={{maxWidth: 'fit-content'}}>
                    <button className='htoc-button'>BROWSE COURSES</button>
                </Link>
            </div>
            <div className="htoc-img">
                <img alt="htoc-img" className='htoc-img' src={htocImg}/>
            </div>
        </div>
    );
}

export default HToC;