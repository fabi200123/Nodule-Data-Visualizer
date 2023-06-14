import React from 'react';
import { MdArrowBack } from "react-icons/md";
import { Patient as PatientModel } from "../models/patient";
import stylePatient from "../styles/ViewPatient.module.css";

interface ViewPatientProps {
    patient: PatientModel,
    dashAppContent: string;
    goBack: () => void;
}

const ViewPatientCT: React.FC<ViewPatientProps> = ({ patient, dashAppContent, goBack }) => {
     const { name, cnp } = patient; // Destructure the name and cnp from the patient object

    return (
    <>
        <MdArrowBack
            style={{height: '5vh', width: '5vw', overflow: 'auto'}}
            onClick={goBack}
        /> <br/>
        <label className={`${stylePatient.patientDetails}`}>
            Name: {name}
        </label>
        <label className={`${stylePatient.patientDetails}`}>
            CNP: {cnp}
        </label> <br/>
        <div style={{height: '80vh', width: '100vw', overflow: 'auto'}}>
        <iframe
            srcDoc={dashAppContent}
            title="Dash App"
            width="100%"
            height="100%"
            style={{border: 'none'}}
        />
        </div>
    </>
  );
};

export default ViewPatientCT;
