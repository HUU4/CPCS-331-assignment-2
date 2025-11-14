# Semantic Network – Vehicle Domain (CPCS-331)

This repository contains a semantic network implementation for the **Vehicle** domain, developed for Assignment 2 in CPCS-331 (Artificial Intelligence).  
The project demonstrates how knowledge can be represented using nodes and labeled relationships, with support for inference and conflict detection.

---

## 📘 Project Overview

A **semantic network** is a graph-based knowledge representation technique where:
- **Nodes** represent concepts, objects, or attributes.
- **Edges** represent labeled relationships (e.g., *is-a*, *has-part*, *uses-fuel*).

This project models a simple domain of vehicles (Car, Truck, Electric Car, etc.) and their properties.

---

## ✔ Implemented Features

### 1. **Basic Operations (Required)**
- Add nodes (concepts, parts, fuel types)
- Add relationships (`is-a`, `has-part`, `uses-fuel`)
- Remove nodes and relationships
- Query / search functions to retrieve:
  - Relations from a source node  
  - Incoming relations to a target node  
  - All nodes of a specific type (concept, part, fuel)

### 2. **Visualization**
Using **NetworkX** and **Matplotlib**, the network is drawn with:
- Blue = concepts  
- Green = parts  
- Pink = fuel types  

Two visualizations are shown:
- Graph **before** inference  
- Graph **after** inference

### 3. **Advanced Features (Optional)**
- **Property Inheritance:**  
  Allows a child node to automatically inherit certain relations from its parent.  
  Example: If *Vehicle has-part Wheel*, then *Car* automatically inherits *has-part Wheel*.

- **Conflict Detection:**  
  Identifies nodes that have multiple conflicting values for the same relation (e.g., a vehicle using more than one fuel type).

---

## 📂 Files Included

semantic_net.py # SemanticNet class (logic, queries, inference, conflicts)
vehicle_example.py # Builds the vehicle domain and shows graphs before/after inference

---

## 🚗 Vehicle Domain (Example)

**Concepts:**  
Vehicle, Car, Truck, Electric Car

**Parts:**  
Engine, Wheel, Battery

**Fuels:**  
Petrol, Diesel, Electricity

**Relations:**  
- Car is-a Vehicle  
- Truck is-a Vehicle  
- Electric Car is-a Car  
- Vehicle has-part Engine  
- Vehicle has-part Wheel  
- Electric Car has-part Battery  
- Car uses-fuel Petrol  
- Truck uses-fuel Diesel  
- Electric Car uses-fuel Electricity  

---

## ▶️ Running the Project

Install dependencies:

```bash
pip install networkx matplotlib
gi
