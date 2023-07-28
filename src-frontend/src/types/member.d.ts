export enum MemberState {
  noob = 'Needs Induction',
  active = 'Active',
  inactive = 'Inactive',
  accountonly = 'Account Only',
}

export type MemberStateStrings = 'noob' | 'active' | 'inactive' | 'accountonly';
export type MemberStateDisplayStrings =
  | 'Needs Induction'
  | 'Active'
  | 'Inactive'
  | 'Account Only';

export enum MemberSubscriptionState {
  inactive = 'Inactive',
  active = 'Active',
  cancelling = 'Cancelling',
}

interface MemberProfile {
  id: number;
  admin: boolean;
  superuser: boolean;
  email: string;
  excludeFromEmailExport: boolean;
  registrationDate: string;
  lastUpdatedProfile: string;
  screenName: string;
  name: {
    first: string;
    last: string;
    full: string;
  };
  phone: string;
  state: MemberState;
  vehicleRegistrationPlate: string;
  rfid: string;
  memberBucks: {
    balance: number;
    lastPurchase: string | null;
  };
  updateProfileRequired: boolean;
  lastSeen: string | null;
  lastInduction: string | null;
  stripe: {
    cardExpiry: string;
    last4: string;
  };
  subscriptionStatus: MemberSubscriptionState;
}

export enum MemberTransactionType {
  stripe = 'Stripe Top-up',
  bank = 'Bank Transfer',
  cash = 'Cash',
  card = 'Membership Card',
  other = 'Other',
}

interface MemberbucksTransaction {
  amount: number;
  type: MemberTransactionType;
  description: string;
  date: Date;
}

interface MemberBillingInfo {
  subscription: MemberSubscription | null;
  memberbucks: {
    balance: number;
    stripe_card_last_digits: string;
    stripe_card_expiry: string;
    transactions: MemberbucksTransaction[];
    lastPurchase: Date;
  };
}
