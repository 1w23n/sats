package main

import (
    "fmt"
    "net/http"
)

func ServerHTTP(w http.ResponseWriter, r *http.Request) {
    var text string
    text = "Hello, World"
    w.Write([]byte(text))
}

func main() {
    http.HandleFunc("/", ServerHTTP)
    fmt.Println("Web Server Start!")
    err := http.ListenAndServe("0.0.0.0:8081", nil)
    if err != nil {
        fmt.Println("Error!")
    }
}
