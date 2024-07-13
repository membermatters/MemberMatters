import { z } from 'zod';
import {
  MemberSubscription,
  SubscriptionStateSchema,
} from 'types/subscriptions';

export const MemberStateSchema = z.enum([
  'noob',
  'active',
  'inactive',
  'accountonly',
]);
export type MemberState = z.infer<typeof MemberStateSchema>;

export const MemberProfileSchema = z.object({
  id: z.number(),
  admin: z.boolean(),
  email: z.string(),
  excludeFromEmailExport: z.boolean(),
  registrationDate: z.string(),
  lastUpdatedProfile: z.string(),
  screenName: z.string(),
  name: z.object({
    first: z.string(),
    last: z.string(),
    full: z.string(),
  }),
  phone: z.string(),
  state: MemberStateSchema,
  vehicleRegistrationPlate: z.string(),
  rfid: z.string(),
  memberBucks: z.object({
    balance: z.number(),
    lastPurchase: z.string().nullable(),
  }),
  updateProfileRequired: z.boolean(),
  lastSeen: z.string().nullable(),
  lastInduction: z.string().nullable(),
  stripe: z.object({
    cardExpiry: z.string(),
    last4: z.string(),
  }),
  subscriptionStatus: SubscriptionStateSchema,
});

export type MemberProfile = z.infer<typeof MemberProfileSchema>;

export enum MemberTransactionType {
  stripe = 'Stripe Top-up',
  bank = 'Bank Transfer',
  cash = 'Cash',
  card = 'Membership Card',
  other = 'Other',
}
export const MemberTransactionTypeSchema = z.nativeEnum(MemberTransactionType);

export const MemberbucksTransactionSchema = z.object({
  amount: z.number(),
  type: MemberTransactionTypeSchema,
  description: z.string(),
  date: z.date(),
});

export type MemberbucksTransaction = z.infer<
  typeof MemberbucksTransactionSchema
>;

export const MemberBillingInfoSchema = z.object({
  subscription: z
    .object({
      status: SubscriptionStateSchema,
      plan: z.string(),
      startDate: z.date(),
      endDate: z.date(),
    })
    .nullable(),
  memberbucks: z.object({
    balance: z.number(),
    stripe_card_last_digits: z.string(),
    stripe_card_expiry: z.string(),
    transactions: z.array(MemberbucksTransactionSchema),
    lastPurchase: z.date(),
  }),
});

export interface MemberBillingInfo {
  subscription: MemberSubscription | null;
  memberbucks: {
    balance: number;
    stripe_card_last_digits: string;
    stripe_card_expiry: string;
    transactions: MemberbucksTransaction[];
    lastPurchase: Date;
  };
}
