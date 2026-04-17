// @title Your API
// @version 1.0
// @description REST API with Swagger
// @host localhost:8080
// @BasePath /

package main

import (
    "net/http"

    "github.com/gin-gonic/gin"
)

// PingExample godoc
// @Summary Ping the server
// @Description Simple ping endpoint
// @Tags healthcheck
// @Accept json
// @Produce json
// @Success 200 {object} map[string]string
// @Router /ping [get]
func Ping(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
        "message": "pong",
    })
}
