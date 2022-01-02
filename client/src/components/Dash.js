import React from 'react'

export default function Dash() {
    return (
        <div className="text-center">
            <iframe 
                style={{width:'100%',height:'100vh'}} 
                title="Online Web Articles Visualization" 
                src="https://app.powerbi.com/reportEmbed?reportId=df3cf7be-bb0e-497b-93c1-2ef11bcc45a3&autoAuth=true&ctid=eb12f8ec-35f2-415d-97bf-0e34301876a7&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLXdlc3QtZXVyb3BlLWItcHJpbWFyeS1yZWRpcmVjdC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D" 
                frameborder="0" 
                allowFullScreen="true"
            />
        </div>
    )
}



