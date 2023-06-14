import "dotenv/config";
import express, { NextFunction, Request, Response } from "express";
import notesRoutes from "./routes/notes";
import userRoutes from "./routes/users";
import patientsRoutes from "./routes/patient";
import requestsRoutes from "./routes/requests";
import uploadRoute from './routes/upload';
import morgan from "morgan";
import createHttpError, { isHttpError } from "http-errors";
import session from "express-session";
import env from "./util/validateEnv";
import MongoStore from "connect-mongo";
import { requiresAuth } from "./middleware/auth";
import path from 'path';


const app = express();

app.use(morgan("dev"));

app.use(express.json());

// Serve static files from the frontend build directory
app.use(express.static(path.resolve(__dirname, '../../frontend/build')));

app.use(session({
    secret: env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        maxAge: 60 * 60 * 1000,
    },
    rolling: true,
    store: MongoStore.create({
        mongoUrl: env.MONGO_CONNECTION_STRING
    }),
}));

app.get('/', (req, res) => {
   res.sendFile(path.join(__dirname, '../../frontend/build', 'index.html'));

});

app.use("/api/users", userRoutes);
app.use("/api/notes", requiresAuth, notesRoutes);
app.use("/api/requests", requiresAuth, requestsRoutes);
app.use("/api/patients", requiresAuth, patientsRoutes);
app.use('/upload', uploadRoute);

app.use((req, res, next) => {
    next(createHttpError(404, "Endpoint not found!"));
});

// eslint-disable-next-line @typescript-eslint/no-unused-vars
app.use((error: unknown, req: Request, res: Response, next: NextFunction) => {
    console.error(error);
    let errorMessage = "An unknown error occurred";
    let statusCode = 500;
    if (isHttpError(error)) {
        statusCode = error.status;
        errorMessage = error.message;
    }
    res.status(statusCode).json({ error: errorMessage });
});

export default app;
