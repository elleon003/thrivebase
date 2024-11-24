import antfu from '@antfu/eslint-config'

export default antfu({
  // Enable Vue support
  vue: true,

  // TypeScript configuration
  typescript: false,

  // Customize rules
  rules: {
    'vue/multi-word-component-names': ['error', {
      ignores: []
    }],
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/component-definition-name-casing': ['error', 'PascalCase'],
    'vue/no-unused-vars': 'error',
    'vue/no-unused-components': 'error',
    'vue/no-template-shadow': 'error',
    'vue/require-default-prop': 'error',
    'vue/require-prop-types': 'error',
    'vue/v-bind-style': ['error', 'shorthand'],
    'vue/v-on-style': ['error', 'shorthand'],
    'vue/no-v-html': 'error',
    'vue/padding-line-between-blocks': 'error',
    'vue/prefer-separate-static-class': 'error',

    // JavaScript rules
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-unused-vars': ['error', { 
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_'
    }],
    'prefer-const': 'error',
    'no-var': 'error',
    'object-shorthand': 'error',
    'array-callback-return': 'error',
    'prefer-template': 'error',
    'template-curly-spacing': ['error', 'never'],
    'space-before-function-paren': ['error', {
      anonymous: 'never',
      named: 'never',
      asyncArrow: 'always'
    }],
    'arrow-parens': ['error', 'always'],
    'no-param-reassign': 'error',
    'prefer-destructuring': ['error', {
      array: true,
      object: true
    }],
    'import/prefer-default-export': 'off',
    'import/no-extraneous-dependencies': ['error', {
      devDependencies: [
        'test/**',
        'tests/**',
        'spec/**',
        '**/__tests__/**',
        '**/__mocks__/**',
        'vite.config.js',
        'vitest.config.js',
        'jest.config.js',
        '.eslintrc.js',
        '.prettierrc.js'
      ],
      optionalDependencies: false
    }]
  },

  // Files to ignore
  ignores: [
    'dist',
    'node_modules',
    '*.min.js',
    'coverage',
    'public'
  ]
})
