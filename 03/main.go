package main


import (
	"fmt"
	"time"
	"context"
	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/bson/primitive"
)
type Todo struct {
	Id primitive.ObjectID `bson:"_id,omitempty" json:"id,omitempty"`
	Title string 
	Desc string
	Date  time.Time
}


func getC() (*mongo.Collection){
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")

	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		fmt.Println(err)
		return nil
	}

	err = client.Ping(context.TODO(), nil)
	if err != nil {
		fmt.Println(err)
		return nil
	}

	collection := client.Database("test").Collection("todo")
	return collection
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
	initRoute()
}
func delete(c *gin.Context) {
	id := c.Params.ByName("id")
	objID, _ := primitive.ObjectIDFromHex(id)
	collection:=getC()
	_, err := collection.DeleteMany(context.TODO(), bson.D{{"_id", objID}})
	if err != nil {
		fmt.Println(err)
	}
	c.JSON(204, "")
}
func update(c *gin.Context) {
	var todo Todo
	c.BindJSON(&todo)
	id := c.Params.ByName("id")
	objID, _ := primitive.ObjectIDFromHex(id)

	filter := bson.D{{"_id", objID}}

	update := bson.D{
		{"$set", bson.D{
			{"title", todo.Title},
			{"desc", todo.Desc},
		}},
	}
	collection:=getC()
	_, err := collection.UpdateOne(context.TODO(), filter, update)
	if err != nil {
		fmt.Println(err)
	}

	filter = bson.D{{"_id", objID}}
	collection.FindOne(context.TODO(), filter).Decode(&todo)
	c.JSON(200, todo)
}
func create(c *gin.Context) {
	var todo Todo
	c.BindJSON(&todo)
	
	collection:=getC()
	r, err := collection.InsertOne(context.TODO(), todo)
	if err != nil {
		fmt.Println(err)
	}

	id:=r.InsertedID
	filter := bson.D{{"_id", id}}
	collection.FindOne(context.TODO(), filter).Decode(&todo)
	c.JSON(201, todo)

}
func getById(c *gin.Context) {
	id := c.Params.ByName("id")
	objID, _ := primitive.ObjectIDFromHex(id)
	filter := bson.D{{"_id", objID}}
	var todo Todo
	collection := getC()
	err := collection.FindOne(context.TODO(), filter).Decode(&todo)
	if err != nil {
		fmt.Println(err)
	}else{
		c.JSON(200, todo)
	}
}
func getAll(c *gin.Context) {
	var todos []*Todo
	collection := getC()
	cur, err := collection.Find(context.TODO(), bson.D{{}})
	if err != nil {
		fmt.Println(err)
	}

	for cur.Next(context.TODO()) {
		var elem Todo
		err := cur.Decode(&elem)
		if err != nil {
			fmt.Println(err)
			return
		}

		todos = append(todos, &elem)
	}

	if err := cur.Err(); err != nil {
		fmt.Println(err)
	}
	// Close the cursor once finished
	cur.Close(context.TODO())
	c.JSON(200, todos)
}