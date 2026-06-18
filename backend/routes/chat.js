const express = require("express");
const axios = require("axios");

const router = express.Router();

router.post("/", async (req, res) => {

    try {

        const response =
            await axios.post(
                "http://127.0.0.1:5001/chat",
                req.body
            );

        res.json(response.data);

    } catch (error) {

        console.error(error);

        res.status(500).json({
            error: "Agent unavailable"
        });
    }
});

module.exports = router;