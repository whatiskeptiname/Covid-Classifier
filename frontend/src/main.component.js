import React, { useState } from "react";
import axios from "axios";
import { VictoryPie } from "victory-pie";

import "./main.component.css";

export default function MainComponent() {
  const [image, setImage] = useState({ preview: "" });
  const [selectedFile, setSelectedFile] = React.useState(null);
  const [data, setdata] = React.useState({
    label: "",
    covidData: "",
    normalData: "",
  });
  const [result, setResult] = React.useState(false);
  const handleChange = (e) => {
    setImage({
      preview: URL.createObjectURL(e.target.files[0]),
    });
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append("file", selectedFile);
    const url = "http://127.0.0.1:8000/predict/";
    const config = {
      headers: { "content-type": "multipart/form-data" },
    };
    axios
      .post(url, formData, config)
      .then((response) => {
        setResult(true);
        setdata({
          label: response.data.class[0],
          covidData: response.data.class[1],
          normalData: response.data.class[2],
        });
      })
      .catch((error) => {
        console.log("error: ", error);
      });
  };
  const newPhoto = () => {
    setResult(false);
    setImage({
      preview: "",
    });
  };
  return (
    <div
      style={{
        position: "absolute",
        top: "30%",
        left: "50%",
        marginTop: "-100px",
        marginLeft: "-170px",
        padding: "10px",
        border: "4px dashed rgb(124, 123, 123)",
      }}
    >
      <label htmlFor="upload-button">
        {image.preview ? (
          <>
            <img
              src={image.preview}
              alt="dummy"
              width="300"
              height="300"
              className="image"
            />
            {result ? (
              ""
            ) : (
              <p className="text-center" style={{ cursor: "pointer" }}>
                Click Here To Upload Again
              </p>
            )}
          </>
        ) : (
          <>
            <h5
              className="text-center"
              style={{
                lineHeight: "170px",
                color: "black",
                fontFamily: "Arial",
                fontSize: "20px",
                cursor: "pointer",
              }}
            >
              Drag your X-Ray here or Click in this area.
            </h5>
          </>
        )}
      </label>
      <input
        type="file"
        id="upload-button"
        style={{ display: "none" }}
        onChange={handleChange}
      />
      {result ? (
        ""
      ) : image.preview ? (
        <button onClick={handleUpload} style={{ cursor: "pointer" }}>
          Upload
        </button>
      ) : (
        ""
      )}
      {result ? (
        <>
          <h1>
            Report:
            {data.label}
          </h1>
          <VictoryPie
            data={[
              {
                x: `Covid:${Math.round(data.covidData)}%`,
                y: Math.round(data.covidData),
              },
              {
                x: `Normal:${Math.round(data.normalData)}%`,
                y: Math.round(data.normalData),
              },
            ]}
            colorScale={[" #ae163e", "#104323"]}
            radius={100}
          />
          <div style={{ display: "flex", flexDirection: "row" }}>
            <div style={{ display: "flex", flexDirection: "row" }}>
              <div class="box blue"></div>{" "}
              <p style={{ marginTop: "-7px" }}>Normal</p>
            </div>

            <div style={{ display: "flex", flexDirection: "row" }}>
              <div class="box wine"></div>{" "}
              <p style={{ marginTop: "-7px" }}>Covid</p>
            </div>
          </div>
        </>
      ) : (
        ""
      )}
      {result ? (
        <button
          style={{ marginTop: "50px", width: "250px", cursor: "pointer" }}
          onClick={newPhoto}
        >
          Click Here To Upload New X-Ray
        </button>
      ) : (
        ""
      )}
    </div>
  );
}
