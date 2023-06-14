/// <reference types="node" /
import https from 'https';
import fs from 'fs';
import app from "./app";
import env from "./util/validateEnv";
import mongoose from "mongoose";
import path from 'path';

const port = env.PORT;

// read the certificate and private key
const options = {
  key: fs.readFileSync('./certs/sslkey.pem'),
  cert: fs.readFileSync('./certs/cert.pem')
};

mongoose.connect(env.MONGO_CONNECTION_STRING)
  .then(() => {
    console.log("mongoose connected");

    // create an HTTPS server
    const server = https.createServer(options, app);

    server.listen(port, () => {
      console.log("server running on port: " + port);
    });
  })
  .catch(console.error);
