import { SampleCourses } from "./Samples";
import { Link } from "react-router-dom";

const CourseList = () => {
    return (
        <div className="course-list-section">
            {SampleCourses.map((item, index) => (
                <div className="course-block" key={index}>
                    <div className="course-img-block">
                        <img className="course-img" alt="course-img"/>
                    </div>
                    <div className="course-text-block">
                        <div className="course-title">{item.coursename}</div>
                        <div className="course-offeredby">{item.offeredby}</div>
                    </div>
                    <div className="course-button-block">
                        <Link to={item.courseLink} style={{ maxWidth: 'fit-content' }} target="_blank">
                            <button className="course-button">REGISTER NOW</button>
                        </Link>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default CourseList;
