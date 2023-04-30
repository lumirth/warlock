// sortByField.ts
type Sortable = {
    [key: string]: number | string | null;
  };
  
  const isValidArray = (results: Sortable[]): boolean => 
    results && Array.isArray(results) && results.length > 0;
  
  const isFieldValid = (results: Sortable[], field: string): boolean => 
    typeof results[0][field] !== "undefined";
  
  const getFieldValue = (item: Sortable, field: string): number | string => 
    item[field] === null ? 0 : item[field] as number | string;
  
  const isAlreadySorted = (results: Sortable[], field: string): boolean => {
    for (let i = 0; i < results.length - 1; i++) {
      const currentValue = getFieldValue(results[i], field);
      const nextValue = getFieldValue(results[i + 1], field);
      if (currentValue < nextValue) {
        return false;
      }
    }
    return true;
  };
  
  const sortByNumbers = (
    a: Sortable,
    b: Sortable,
    field: string,
    fallbackField: string | undefined,
    reverseOrder: boolean
  ): number => {
    const aValue = getFieldValue(a, field) as number;
    const bValue = getFieldValue(b, field) as number;
    const comparison = reverseOrder ? aValue - bValue : bValue - aValue;
    if (aValue !== bValue) {
      return comparison;
    } else if (
      fallbackField &&
      typeof a[fallbackField] !== "undefined" &&
      typeof b[fallbackField] !== "undefined"
    ) {
      return String(b[fallbackField]).localeCompare(String(a[fallbackField]));
    } else {
      return 0;
    }
  };
  
  const sortByStrings = (
    a: Sortable,
    b: Sortable,
    field: string,
    fallbackField: string | undefined,
    reverseOrder: boolean
  ): number => {
    const aValue = String(getFieldValue(a, field));
    const bValue = String(getFieldValue(b, field));
    const compareResult = bValue.localeCompare(aValue);
    const comparison = reverseOrder ? -compareResult : compareResult;
    if (compareResult !== 0) {
      return comparison;
    } else if (
      fallbackField &&
      typeof a[fallbackField] !== "undefined" &&
      typeof b[fallbackField] !== "undefined"
    ) {
      return String(b[fallbackField]).localeCompare(String(a[fallbackField]));
    } else {
      return 0;
    }
  };
  
  const sortByField = (
    results: Sortable[],
    field: string,
    fallbackField?: string,
    reverseOrder = false
  ): Sortable[] | undefined => {
    if (!isValidArray(results)) {
      console.error("The provided array is either empty or not an array.");
      return undefined;
    }
  
    if (!isFieldValid(results, field)) {
      console.error(`The field '${field}' does not exist in the objects.`);
      return undefined;
    }
  
    if (isAlreadySorted(results, field)) {
      results.reverse();
    } else {
      results.sort((a: Sortable, b: Sortable) => {
        const aValue = getFieldValue(a, field);
        const bValue = getFieldValue(b, field);
  
        if (typeof aValue === "number" && typeof bValue === "number") {
          return sortByNumbers(a, b, field, fallbackField, reverseOrder);
        } else {
          return sortByStrings(a, b, field, fallbackField, reverseOrder);
        }
      });
    }
  
    return results;
  };
  
  export { sortByField };
  