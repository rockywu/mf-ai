
let canUseStorage = true;
try {
    uni.setStorageSync("app-key-testinstall", "app-key-testinstall");
} catch (e) {
    canUseStorage = false;
}

export function getStorageSync(key) {
    return uni.getStorageSync(key)
}

export function setStorageSync(key, value) {
    return uni.setStorageSync(key, value);
}

export function removeStorageSync(key) {
    return uni.removeStorageSync(key);
}

export const Storage = function (name, prefix = "mm-") {
    if (!(this instanceof Storage)) {
        return new Storage(name, prefix);
    }
    let key = prefix + name;
    return {
        get() {
            if (Storage._cache[key] !== undefined) {
                return Storage._cache[key];
            }
            let data = getStorageSync(key);
            try {
                data = JSON.parse(data);
                Storage._cache[key] = data;
                return data;
            } catch (e) {
                return null;
            }
        },
        set(data) {
            try {
                setStorageSync(key, JSON.stringify(data));
                Storage._cache[key] = data;
                return true;
            } catch (e) {
                return false;
            }
        },
        remove() {
            Storage._cache[key] = undefined;
            removeStorageSync(key);
        },
    };
}

Storage._cache = {};


export const request = (params) => {
    return uni.request(params)
}