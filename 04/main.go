package main


import (
	"fmt"
	"time"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	// "net/http"
	"github.com/gin-gonic/gin"
)
type Todo struct {
    ID        int  `gorm:"AUTO_INCREMENT"`
    Title     string 
    Desc  string 
    CreatedAt time.Time 
}

var _db *gorm.DB
var _err error
func opendb(){
	dsn := "root:{pwd}@tcp(127.0.0.1:3306)/test?charset=utf8mb4&parseTime=True&loc=Local"
	_db, _err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if _err != nil {
		fmt.Println(_err)
	}
	
	fmt.Println("connected db")
}
func initRoute(){
	r := gin.Default()
	r.GET("/todo/", getAll)
	r.GET("/todo/:id", getById)
	r.POST("/todo", create)
	r.PUT("/todo/:id", update)
	r.DELETE("/todo/:id", delete)
	r.Run(":3000")
}
func main() {
	opendb()
	initRoute()
}
func delete(c *gin.Context) {
	id := c.Params.ByName("id")
	var todo Todo
	_ = _db.Where("id = ?", id).Delete(&todo)
	c.JSON(204, "")
}
func update(c *gin.Context) {
	var todo Todo
	id := c.Params.ByName("id")
	if err := _db.Where("id = ?", id).First(&todo).Error; err != nil {
		c.AbortWithStatus(404)
		fmt.Println(err)
	}
	c.BindJSON(&todo)
	_db.Save(&todo)
	c.JSON(200, todo)
}
func create(c *gin.Context) {
	var todo Todo
	c.BindJSON(&todo)
	_db.Create(&todo)
	c.JSON(201, todo)

}
func getById(c *gin.Context) {
	id := c.Params.ByName("id")
	var todo Todo
	if err := _db.Where("id = ?", id).First(&todo).Error; err != nil {
		c.AbortWithStatus(404)
		fmt.Println(err)
	} else {
		c.JSON(200, todo)
	}
}
func getAll(c *gin.Context) {
	var todos []Todo
	if err := _db.Find(&todos).Error; err != nil {
		c.AbortWithStatus(404)
		fmt.Println(err)
	} else {
		c.JSON(200, todos)
	}
}