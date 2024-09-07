# Test Plan for API Testing with JSONPlaceholder

## Project Name
API Testing with JSONPlaceholder

## Prepared By
Nav Durg Raman Pratap Singh

## Version
1.0

## Date
Sept 1, 2024

## 1. Introduction
This test plan outlines the approach for testing various HTTP request methods on the [JSONPlaceholder API](https://jsonplaceholder.typicode.com). The focus is on validating the structure, content, and expected outcomes of the API responses.

## 2. Objectives
- Validate API response structure and content.
- Ensure correct HTTP status codes for each request.
- Test API behavior with valid and invalid resources.

## 3. Scope
- **In-Scope:** 
  - GET, POST, PUT, PATCH, DELETE methods
  - Valid and invalid scenarios
- **Out-of-Scope:** 
  - Performance and security testing

## 4. Test Environment
- **API Endpoint:** https://jsonplaceholder.typicode.com
- **Language:** Python
- **Libraries:** `requests`, `pytest`
- **OS:** [Your OS]

## 5. Assumptions
- API is stable and accessible.
- Test environment is properly configured.

## 6. Test Cases

| **ID** | **Description**                                      | **Preconditions**  | **Steps**                                                   | **Expected Result**                                           | **Status** |
|--------|------------------------------------------------------|--------------------|-------------------------------------------------------------|----------------------------------------------------------------|------------|
| TC01   | Validate fetching a specific TODO item               | API accessible     | Send GET request to `/todos/1`                               | 200 status, correct structure and content                      | Pass/Fail  |
| TC02   | Validate creating a new post with POST               | API accessible     | Send POST request to `/posts`                                | 201 status, correct structure and content                      | Pass/Fail  |
| TC03   | Validate updating an existing post with PUT          | API accessible     | Send PUT request to `/posts/1`                               | 200 status, correct structure and content                      | Pass/Fail  |
| TC04   | Validate partially updating a post with PATCH        | API accessible     | Send PATCH request to `/posts/1`                             | 200 status, correct title update, other fields unchanged       | Pass/Fail  |
| TC05   | Validate deleting a post with DELETE                 | API accessible     | Send DELETE request to `/posts/1`                            | 200 status                                                     | Pass/Fail  |
| TC06   | Validate fetching posts for a specific user          | API accessible     | Send GET request to `/posts?userId=1`                        | 200 status, all posts belong to `userId=1`                     | Pass/Fail  |
| TC07   | Validate fetching a non-existent TODO item (404)     | API accessible     | Send GET request to `/todos/9999`                            | 404 status                                                     | Pass/Fail  |
| TC08   | Validate updating a post with an invalid ID (404)    | API accessible     | Send PUT request to `/posts/9999`                            | 404 status                                                     | Pass/Fail  |

## 7. Exit Criteria
- All test cases executed, defects documented.

## 8. Reporting
- Results documented, including test case statuses and defects.

## 9. Risks and Mitigation

| **Risk**                  | **Impact** | **Mitigation** |
|---------------------------|------------|----------------|
| API down or inaccessible   | High       | Reschedule testing |
| Incorrect environment setup | Medium     | Verify setup before testing |

## 10. Approval

| **Name**         | **Title**           | **Signature** | **Date**        |
|------------------|---------------------|---------------|-----------------|
| Nav Durg Raman Pratap Singh      | QA Engineer         |               | [Approval Date] |

