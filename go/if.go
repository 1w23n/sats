package main

import (
    "fmt"
    "time"
)

func main() {
    hour := time.Now().Hour()
    if hour >= 6 && hour < 12 {
        fmt.Println("朝です")
    } else if hour < 19 {
        fmt.Println("昼です")
    } else {
        fmt.Println("夜です")
    }
}
