import React from "react";

const urlGithub = "https://github.com/AlexisIvan2000";
const urlLinkedin = "https://www.linkedin.com/in/alexis-moungang-396104371";
const urlSnapchat =
  "https://www.snapchat.com/add/alexis_ivan00?share_id=bmC_7yVomHY&locale=en-CA";

export function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p className="footer-text">© 2025 MyspotR All rights reserved.</p>
        <div className="footer-social">
          <a
            href={urlGithub}
            target="_blank"
            rel="noopener noreferrer"
            className="social-item"
          >
            <i className="fab fa-github"></i>
            <p>Github</p>
          </a>

         <a
            href={urlLinkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="social-item"
          >
            <i className="fab fa-github"></i>
            <p>Linkedln</p>
          </a>
          <a
            href={urlSnapchat}
            target="_blank"
            rel="noopener noreferrer"
            className="social-item"
          >
            <i className="fab fa-github"></i>
            <p>Snapchat</p>
          </a>
        </div>
      </div>
    </footer>
  );
}
