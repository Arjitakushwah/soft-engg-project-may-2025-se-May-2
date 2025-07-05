// src/setup.js
export function initializeDummyData() {
    // Check if data already exists
    const hasParent = localStorage.getItem('parent')
    const hasChildren = localStorage.getItem('childList')
  
    if (!hasParent) {
      // Add dummy parent
      const dummyParent = {
        username: 'parent001',
        password: 'parentpass',
        name: 'Parent One',
        email: 'parent1@example.com'
      }
      localStorage.setItem('parent', JSON.stringify(dummyParent))
  
    //   // Simulate parent login
    //   localStorage.setItem('userRole', 'parent')
    //   localStorage.setItem('username', dummyParent.name)
    }
  
    if (!hasChildren) {
      // Add dummy children for the parent
      const dummyChildren = [
        {
          id: 1,
          parentUsername: 'parent001',
          username: 'child001',
          password: 'childpass1',
          name: 'Alice',
          age: 9,
          gender: 'Female'
        },
        {
          id: 2,
          parentUsername: 'parent001',
          username: 'child002',
          password: 'childpass2',
          name: 'Bob',
          age: 11,
          gender: 'Male'
        }
      ]
      localStorage.setItem('childList', JSON.stringify(dummyChildren))
    }
  }
  