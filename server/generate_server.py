#!/usr/bin/env python3

import os.path
from os import path
import os
from pathlib import Path

# ----------------------------------------- Set according to current directory ----------------------------
current_path = (Path.cwd())

# ------------------------------------------- Global Variables ---------------------------------------------
users_choice = "yes"
db_items = []

# ------------------------------------------------------ functions -----------------------------------------------
def create_config_files():
    config_file = 'const mongoose = require("mongoose");const connectDB = async () => {  await mongoose.connect(process.env.MONGO_URI, {    useNewUrlParser: true,    useUnifiedTopology: true, }); console.log("✅ Database connected");};module.exports = connectDB;'
    config_file_path = config_directory + "/mongoose.js"
    try:
        print("i 🛑 tried")
        write_to_file(config_file_path, config_file)
        return print("Config Files Successfully Created...")
    except:
        return print("Something Went Wrong When Creating Config Files...")

def create_controller_files(name, *args):
    controller_first = 'const '+name+' = require("../models/'+name+'"); exports.create'+name+' = async (req, res) => { const page = req.query.page || 0;const limit = req.query.limit || 25; try { let new'+name+' = new '+name+'({'
    controller_second = []
    controller_third = ' }); await new'+name+'.save(); res.send(new'+name+'); } catch (err) { console.log(err); } }; exports.read'+name+' = async (req, res) => { try { '+name+'.find({}, (err, result) => { if (err) { res.json({ app: err }); } res.send(result); }).sort().skip(page * limit).limit(limit); } catch (err) { console.log(err); } }; exports.read'+name+'FromID = async (req, res) => { try { await '+name+'.findById({ _id: req.params.id }, {}, (err, result) => { if (err) { res.json({ app: err }); } res.send(result); }); } catch (err) { console.log(err); } }; exports.update'+name+' = async (req, res) => { try { await '+name+'.findByIdAndUpdate( req.params.id, {'
    controller_fourth = []
    controller_fifth = ' }, (err, result) => { if (err) { res.json({ app: err }); } res.send(result); } ); } catch (err) { console.log(err); } }; exports.delete'+name+' = async (req, res) => { try { if ((await '+name+'.findById(req.params.id)) === null) { res.json({ app: "post not found" }); } else { await '+name+'.findByIdAndRemove(req.params.id).exec(); res.json({ app: "post deleted" }); } } catch (err) { console.log(err); res.send(err); } };'
    controller_file_path = controller_directory + f'/{name}.js'
    for arg in args:
        for a in arg:
            file = ''+ a +': req.body.'+ a +','
            controller_second.append(file)
            controller_fourth.append(file)   
    try:
        entire_file = controller_first + ''.join(controller_second) + controller_third + ''.join(controller_fourth) + controller_fifth
        write_to_file(controller_file_path, entire_file)
        return print("Controller Files Successfully Created...")
    except:
        return print("Something Went Wrong When Creating Controller Files...")

def create_models_files(name, *args):
    models_file_first = 'const mongoose = require("mongoose"); const '+name+'Schema = new mongoose.Schema( {'
    models_file_middle = []
    models_file_last = ' }, { timestamps: true } ); const '+name+' = mongoose.model("'+name+'", '+name+'Schema); module.exports = '+name+';'
    models_file_path = model_directory + f'/{name}.js'
    for arg in args:
        for a in arg:
            middle = ''+ a + ': { type: String, required: [true, "Please provide '+ a + '"],  },'
            models_file_middle.append(middle)
    try:
        middle_file = ''.join(models_file_middle)
        entire_file = models_file_first + middle_file + models_file_last
        write_to_file(models_file_path, entire_file)
        return print("models Files Successfully Created...")
    except:
        return print("Something Went Wrong When Creating Model Files...")


def create_routes_files(name):
    routes_file = 'const express = require("express"); const router = express.Router(); const { create'+name+', read'+name+', read'+name+'FromID, update'+name+', delete'+name+', } = require("../controllers/'+name+'"); router.route("/create").post(create'+name+'); router.route("/read").get(read'+name+'); router.route("/read/:id").get(read'+name+'FromID); router.route("/update/:id").post(update'+name+'); router.route("/delete/:id").delete(delete'+name+'); module.exports = router; '
    routes_file_path = route_directory + f'/{name}.js'
    try:
        write_to_file(routes_file_path, routes_file)
        return print("routes Files Successfully Created...")
    except:
        return print("Something Went Wrong When Creating routes Files...")
        
def create_index_file(name):
    index_file = 'const express = require("express"); const session = require("express-session");  const app = express(); const cors = require("cors"); const PORT = process.env.PORT || 3002;  const connectDB = require("./config/mongoose"); require("dotenv").config({ path: "./.env" }); app.use(express.json()); app.use(express.urlencoded({ extended: false })); app.use(cors()); connectDB();  app.get("/", (req, res) => { res.json({ app: "running" }); }); app.listen(PORT, () => { console.log("✅ Listening on port " + PORT); }); app.use("/api/' + name + '", require("./routes/' + name + '"));'
    index_file_path = f'{current_path}/index.js'
    # try:
    if path.exists("./index.js"):
      print("index.js file already exists...Appending route...")
      index_file = open("./index.js", "a")
      index_file.write(f"app.use('/api/{name}', require('./routes/{name}'));")
      index_file.close()
    else:
      write_to_file(index_file_path, index_file)
      return print("index.js Files Successfully Created...")
    # except:
        # return print("Something Went Wrong When Creating index.js Files...")

def create_package_file( ):
    package_file = '{ "name": "generate-mongo-db", "version": "1.0.0", "description": "", "main": "index.js", "scripts": { "test": "echo \\"Error: no test specified\\" && exit 1" }, "keywords": [], "author": "", "license": "ISC", "dependencies": { "cors": "^2.8.5", "dotenv": "^16.0.3", "express": "^4.18.2", "express-session": "^1.17.3", "jsonwebtoken": "^8.5.1", "mongoose": "^6.7.0", "mongoose-findorcreate": "^3.0.0", "nodemon": "^2.0.20" } } '
    package_file_path = os.path.join(current_path, 'package.json')
    try:
        write_to_file(package_file_path, package_file)
        return print("package Files Successfully Created...")
    except:
        return print("Something Went Wrong When Creating package Files...")

def write_to_file(path, content):
  file = open(path, "w", encoding="utf-8")
  file.write(content)
  file.close()

# ----------------------------------------- Create folders for all of the files ----------------------------
config_directory = os.path.join(current_path, "config")
controller_directory = os.path.join(current_path, "controllers")
middleware_directory = os.path.join(current_path, "middleware")
model_directory = os.path.join(current_path, "models")
route_directory = os.path.join(current_path, "routes")

print("Creating needed folders...")

if os.path.exists(config_directory):
  print("Config path already exists.")
else:
  os.mkdir(config_directory)

if os.path.exists(controller_directory):
  print("Controller path already exists.")
else:
  os.mkdir(controller_directory)

if os.path.exists(middleware_directory):
  print("Middleware path already exists.")
else:
  os.mkdir(middleware_directory)

if os.path.exists(model_directory):
  print("Model path already exists.")
else:
  os.mkdir(model_directory)

if os.path.exists(route_directory):
  print("Route path already exists.")
else:
  os.mkdir(route_directory)

# ----------------------------------------- Call everything ----------------------------
type_of_db = input("What are you storing in the DB?")
db_item_amount = input("How many objects do you need in each document?")
db_item_amount_list = [0] * int(db_item_amount)
for item in db_item_amount_list:
  db_item_name = input("Name of the object you want in the document?")
  db_items.append(db_item_name)

print("Adding config files...")
create_config_files()
print("Adding controller files...")
create_controller_files(type_of_db, db_items)
print("Adding route files...")
create_routes_files(type_of_db)
print("Adding model files...")
create_models_files(type_of_db, db_items) 
print("Adding index file...")
create_index_file(type_of_db)
print("Adding json package file...")
create_package_file()

print("Your App Is Ready ✅")
