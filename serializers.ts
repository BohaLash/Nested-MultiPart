
/**
 * Rebuilds data in special order and sent as FormData 
 * to include files along with other data in JSON-like format.
 * 
 * @param {object} payload - Raw object from which the FormData will be built
 * @returns {FormData} FormData to be sent to the server
 * 
 * @example
 * Model has fields called `name`, `picture`, and `gallery`.
 * FormData object to be parsed will look like this:
 * ```js
 *    __data: { "name": "Some name", "picture": "__file1", "gallery": ["__file2", "__file3"] }
 *    __file1: (binary)
 *    __file2: (binary)
 *    __file3: (binary)
 * ```
 */
export const buildNestedFormDataWithFiles = (payload: object): FormData => {
    const form_data = new FormData()
    const files: File[] = []

    const fileName = (index: number) => '__file' + index

    const escapeFiles = (data: any) => {
        if (typeof data !== 'object') return data

        if (data?.constructor.name === 'File') {
            files.push(data)
            return fileName(files.length)
        }

        for (const key in data) {
            data[key] = escapeFiles(data[key])
        }

        return data
    }

    form_data.append('__data', JSON.stringify(escapeFiles(payload)))
    files.forEach((file, i) => form_data.append(fileName(i + 1), file))

    return form_data
}
