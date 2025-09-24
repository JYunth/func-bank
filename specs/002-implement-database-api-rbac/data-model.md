# Data Model Specification

## Overview
This document defines the data models and schemas for the Database, API, and RBAC components. The data model is **completely agnostic** - no assumptions are made about table structure, schema, or datatypes. The components must function without knowledge of the underlying data model.

## Agnostic Design Principles
- No predefined table schemas or column structures
- Functions operate on generic dicts and dynamic queries
- Schema inspection and dynamic SQL generation as needed
- Compatibility with any PostgreSQL table structure
- Runtime validation of data types and constraints

## Database Schema Assumptions (Minimal)
- PostgreSQL with SQLAlchemy ORM
- Tables exist and are accessible
- Primary keys are identifiable (typically 'id' column)
- No assumptions about column names, types, or relationships

## RBAC Data Models (Agnostic)
- Users table: structure unknown, roles stored as strings
- Roles are fully customizable, no hierarchy
- Permissions handled dynamically

## API Data Models (Agnostic)
- Request/Response structures are generic dicts
- Multipart requests parsed without schema assumptions

## Relationships (Agnostic)
- No enforced relationships
- Foreign keys handled by caller if needed

## Constraints (Agnostic)
- Scale: 1k-100k records, 10-100 concurrent users
- Optimistic locking: implemented without schema assumptions
- Data types: validated at runtime, no compile-time assumptions

## Feasibility Note
Complete agnosticism is possible using SQLAlchemy's dynamic table reflection and raw SQL execution. If any function requires schema knowledge (e.g., vector search assumes 'embedding' column), it will be noted and may require compromise.